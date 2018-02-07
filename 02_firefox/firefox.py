import avatar2
import angr as a
import logging

firefox_binary = "./firefox"
trigger = "./trigger"

breakpoint_function = "mozilla::WebGLContext::ReadPixelsImpl"

print "[+] Creating the Avatar object"
ava = avatar2.Avatar(arch=avatar2.archs.X86_64)
ava.log.setLevel(logging.INFO)
ava.load_plugin('gdb_memory_map_loader')
ava.load_plugin("x86.segment_registers")

print "[+] Creating the GDBTarget"
gdb = ava.add_target(avatar2.GDBTarget, local_binary=firefox_binary,
                     arguments=trigger)

# setup angr target
print "[+] Creating the AngrTarget"
load_options = {}
angr = ava.add_target(avatar2.AngrTarget, binary=firefox_binary,
                      load_options={'main_opts': {'backend':'elf'}})

print "[+] Initializing the targets"
ava.init_targets()

# Additional setup for GDB
gdb.disable_aslr()

print "[+] Running Firefox until %s" % breakpoint_function
gdb.bp(breakpoint_function, pending=True)

gdb.cont()
gdb.wait()

print "[+] Firefox reached %s" % breakpoint_function
print "[+] Avatar loads the memory ranges"
ava.load_memory_mappings(gdb, forward=True)

print "[+] Switching the execution to angr"
angr.hook_symbols(gdb)

options = a.options.common_options | set([a.options.STRICT_PAGE_ACCESS])
s = angr.angr.factory.avatar_state(angr, load_register_from=gdb,
                                   options=options)

s.regs.rsi = s.solver.BVS("x", 64)
s.regs.rdx = s.solver.BVS("y", 64)
simmgr = angr.angr.factory.simgr(s)

print "[+] Starting symbolic exploration."
while True:
    simmgr.step()
    if len(simmgr.errored) != 0:
        break

print "[+] Done, found error %s" % simmgr.errored[0].error
ava.shutdown()
