from avatar2 import Avatar, ARMV7M, OpenOCDTarget
from IPython import embed

main_addr = 0xD270

avatar = Avatar(output_directory='/tmp/harvey', arch=ARMV7M)
avatar.load_plugin('assembler')

t = avatar.add_target(OpenOCDTarget, openocd_script='plc.cfg',
                      gdb_executable='arm-none-eabi-gdb')

t.init()

t.set_breakpoint(main_addr)
t.cont()
t.wait()

t.inject_asm('b 0x2000250E',addr=0x20001E2E)
t.inject_asm('mov r5,0xfffffffc\n b 0x20001E30',addr=0x2000250E)

t.inject_asm('b 0x20002514',addr=0x20002338)
t.inject_asm('mov r5,0xfffffffd\n mov r4, r5 \n mov r5, 0\nb 0x2000233E',
             addr=0x20002514)

t.cont()
embed()
