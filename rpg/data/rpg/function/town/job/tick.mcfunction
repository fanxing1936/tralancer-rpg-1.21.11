# 选址与建造，一次只处理一座（每秒一次）；#s：0 未建 1 排队 2 在建 3 建好 4 放弃 5 待重修
schedule function rpg:town/job/tick 20t
execute if score #cur rpg_tw matches 1.. run return run function rpg:town/job/step
execute if score #s1 rpg_tw matches 5 run return run function rpg:town/job/re/1
execute if score #s2 rpg_tw matches 5 run return run function rpg:town/job/re/2
execute if score #s3 rpg_tw matches 5 run return run function rpg:town/job/re/3
execute if score #s4 rpg_tw matches 5 run return run function rpg:town/job/re/4
execute if score #s5 rpg_tw matches 5 run return run function rpg:town/job/re/5
execute if score #s6 rpg_tw matches 5 run return run function rpg:town/job/re/6
execute if score #s7 rpg_tw matches 5 run return run function rpg:town/job/re/7
execute if score #s8 rpg_tw matches 5 run return run function rpg:town/job/re/8
execute if score #s9 rpg_tw matches 5 run return run function rpg:town/job/re/9
execute if score #s10 rpg_tw matches 5 run return run function rpg:town/job/re/10
execute if score #s11 rpg_tw matches 5 run return run function rpg:town/job/re/11
execute if score #s12 rpg_tw matches 5 run return run function rpg:town/job/re/12
execute if score #s13 rpg_tw matches 5 run return run function rpg:town/job/re/13
execute if score #s14 rpg_tw matches 5 run return run function rpg:town/job/re/14
execute if score #s15 rpg_tw matches 5 run return run function rpg:town/job/re/15
execute if score #s16 rpg_tw matches 5 run return run function rpg:town/job/re/16
execute if score #s17 rpg_tw matches 5 run return run function rpg:town/job/re/17
execute if score #s18 rpg_tw matches 5 run return run function rpg:town/job/re/18
execute if score #s19 rpg_tw matches 5 run return run function rpg:town/job/re/19
execute if score #s20 rpg_tw matches 5 run return run function rpg:town/job/re/20
execute if score #s1 rpg_tw matches 1 run return run function rpg:town/job/begin {i:1,nx:556,nz:-1712}
execute if score #s2 rpg_tw matches 1 run return run function rpg:town/job/begin {i:2,nx:1456,nz:-1058}
execute if score #s3 rpg_tw matches 1 run return run function rpg:town/job/begin {i:3,nx:1800,nz:0}
execute if score #s4 rpg_tw matches 1 run return run function rpg:town/job/begin {i:4,nx:1456,nz:1058}
execute if score #s5 rpg_tw matches 1 run return run function rpg:town/job/begin {i:5,nx:556,nz:1712}
execute if score #s6 rpg_tw matches 1 run return run function rpg:town/job/begin {i:6,nx:-556,nz:1712}
execute if score #s7 rpg_tw matches 1 run return run function rpg:town/job/begin {i:7,nx:-1456,nz:1058}
execute if score #s8 rpg_tw matches 1 run return run function rpg:town/job/begin {i:8,nx:-1800,nz:0}
execute if score #s9 rpg_tw matches 1 run return run function rpg:town/job/begin {i:9,nx:-1456,nz:-1058}
execute if score #s10 rpg_tw matches 1 run return run function rpg:town/job/begin {i:10,nx:-556,nz:-1712}
execute if score #s11 rpg_tw matches 1 run return run function rpg:town/job/begin {i:11,nx:1051,nz:-3234}
execute if score #s12 rpg_tw matches 1 run return run function rpg:town/job/begin {i:12,nx:2751,nz:-1998}
execute if score #s13 rpg_tw matches 1 run return run function rpg:town/job/begin {i:13,nx:3400,nz:0}
execute if score #s14 rpg_tw matches 1 run return run function rpg:town/job/begin {i:14,nx:2751,nz:1998}
execute if score #s15 rpg_tw matches 1 run return run function rpg:town/job/begin {i:15,nx:1051,nz:3234}
execute if score #s16 rpg_tw matches 1 run return run function rpg:town/job/begin {i:16,nx:-1051,nz:3234}
execute if score #s17 rpg_tw matches 1 run return run function rpg:town/job/begin {i:17,nx:-2751,nz:1998}
execute if score #s18 rpg_tw matches 1 run return run function rpg:town/job/begin {i:18,nx:-3400,nz:0}
execute if score #s19 rpg_tw matches 1 run return run function rpg:town/job/begin {i:19,nx:-2751,nz:-1998}
execute if score #s20 rpg_tw matches 1 run return run function rpg:town/job/begin {i:20,nx:-1051,nz:-3234}
execute if score #s21 rpg_tw matches 1 run return run function rpg:town/job/begin {i:21,nx:2103,nz:-1528}
execute if score #s22 rpg_tw matches 1 run return run function rpg:town/job/begin {i:22,nx:-2103,nz:1528}
execute if score #s23 rpg_tw matches 1 run return run function rpg:town/job/begin {i:23,nx:3479,nz:2527}
execute if score #s24 rpg_tw matches 1 run return run function rpg:town/job/begin {i:24,nx:-2103,nz:-1528}
