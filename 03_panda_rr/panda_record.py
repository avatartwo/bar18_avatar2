from time import sleep
from avatar2 import Avatar, ARMV7M, OpenOCDTarget, PandaTarget

avatar = Avatar(arch=ARMV7M, output_directory='/tmp/panda_rr')
avatar.load_plugin('orchestrator')

nucleo = avatar.add_target(OpenOCDTarget, 
                           openocd_script='nucleo-l152re.cfg',
                           gdb_executable="arm-none-eabi-gdb",
                           gdb_port=1234)

panda = avatar.add_target(PandaTarget, 
                          executable='panda/qemu-system-arm',
                          gdb_executable="arm-none-eabi-gdb",
                          gdb_port=1235)

rom = avatar.add_memory_range(0x08000000, 0x1000000, 'rom', 
                               file='firmware.bin')

ram = avatar.add_memory_range(0x20000000, 0x14000, 'ram')
mmio= avatar.add_memory_range(0x40000000, 0x1000000, 'mmio', 
                               forwarded=True, forwarded_to=nucleo) 

avatar.init_targets()

avatar.start_target = nucleo
avatar.add_transition(0x8005104, nucleo, panda,
                           synced_ranges=[ram], stop=True)
avatar.start_orchestration()

panda.begin_record('panda_record')
avatar.resume_orchestration(blocking=False)

sleep(5) # Let's execute for a while

avatar.stop_orchestration()
panda.end_record()
