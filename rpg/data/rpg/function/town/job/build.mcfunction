# 区块到齐：建（positioned 镇中心）
execute store result storage rpg:town m.h int 1 run scoreboard players get #h0 rpg_tw
execute store result storage rpg:town m.var int 1 run scoreboard players get #v rpg_tw
data modify storage rpg:town m.sfx set value ""
execute if score #v rpg_tw matches 1 run data modify storage rpg:town m.sfx set value "_snow"
execute if score #v rpg_tw matches 2 run data modify storage rpg:town m.sfx set value "_desert"
execute if score #cur rpg_tw matches 1 run data modify storage rpg:town m.f set value "t1"
execute if score #cur rpg_tw matches 2 run data modify storage rpg:town m.f set value "t2"
execute if score #cur rpg_tw matches 3 run data modify storage rpg:town m.f set value "t3"
execute if score #cur rpg_tw matches 4 run data modify storage rpg:town m.f set value "t4"
execute if score #cur rpg_tw matches 5 run data modify storage rpg:town m.f set value "t5"
execute if score #cur rpg_tw matches 6 run data modify storage rpg:town m.f set value "t6"
execute if score #cur rpg_tw matches 7 run data modify storage rpg:town m.f set value "t7"
execute if score #cur rpg_tw matches 8 run data modify storage rpg:town m.f set value "t8"
execute if score #cur rpg_tw matches 9 run data modify storage rpg:town m.f set value "t9"
execute if score #cur rpg_tw matches 10 run data modify storage rpg:town m.f set value "t10"
execute if score #cur rpg_tw matches 11 run data modify storage rpg:town m.f set value "t11"
execute if score #cur rpg_tw matches 12 run data modify storage rpg:town m.f set value "t12"
execute if score #cur rpg_tw matches 13 run data modify storage rpg:town m.f set value "t13"
execute if score #cur rpg_tw matches 14 run data modify storage rpg:town m.f set value "t14"
execute if score #cur rpg_tw matches 15 run data modify storage rpg:town m.f set value "t15"
execute if score #cur rpg_tw matches 16 run data modify storage rpg:town m.f set value "t16"
execute if score #cur rpg_tw matches 17 run data modify storage rpg:town m.f set value "t17"
execute if score #cur rpg_tw matches 18 run data modify storage rpg:town m.f set value "t18"
execute if score #cur rpg_tw matches 19 run data modify storage rpg:town m.f set value "t19"
execute if score #cur rpg_tw matches 20 run data modify storage rpg:town m.f set value "t20"
execute if score #cur rpg_tw matches 21 run data modify storage rpg:town m.f set value "t21"
execute if score #cur rpg_tw matches 22 run data modify storage rpg:town m.f set value "t22"
execute if score #cur rpg_tw matches 23 run data modify storage rpg:town m.f set value "t23"
execute if score #cur rpg_tw matches 24 run data modify storage rpg:town m.f set value "t24"
function rpg:town/job/build_go with storage rpg:town m
scoreboard players operation #built rpg_tw = #cur rpg_tw
function #rpg:town_built
data modify storage rpg:town m.tx set from storage rpg:town m.x
data modify storage rpg:town m.tz set from storage rpg:town m.z
function rpg:town/job/items with storage rpg:town m
function rpg:town/job/big_rem with storage rpg:town m
execute if score #cur rpg_tw matches 1 run function rpg:town/job/camp_at {dx:-147,dz:135}
execute if score #cur rpg_tw matches 2 run function rpg:town/job/camp_at {dx:17,dz:-199}
execute if score #cur rpg_tw matches 3 run function rpg:town/job/camp_at {dx:122,dz:159}
execute if score #cur rpg_tw matches 4 run function rpg:town/job/camp_at {dx:-197,dz:-35}
execute if score #cur rpg_tw matches 5 run function rpg:town/job/camp_at {dx:169,dz:-107}
execute if score #cur rpg_tw matches 6 run function rpg:town/job/camp_at {dx:-52,dz:193}
execute if score #cur rpg_tw matches 7 run function rpg:town/job/camp_at {dx:-92,dz:-177}
execute if score #cur rpg_tw matches 8 run function rpg:town/job/camp_at {dx:188,dz:68}
execute if score #cur rpg_tw matches 9 run function rpg:town/job/camp_at {dx:-185,dz:77}
execute if score #cur rpg_tw matches 10 run function rpg:town/job/camp_at {dx:85,dz:-181}
execute if score #cur rpg_tw matches 11 run function rpg:town/job/camp_at {dx:60,dz:191}
execute if score #cur rpg_tw matches 12 run function rpg:town/job/camp_at {dx:-173,dz:-100}
execute if score #cur rpg_tw matches 13 run function rpg:town/job/camp_at {dx:195,dz:-43}
execute if score #cur rpg_tw matches 14 run function rpg:town/job/camp_at {dx:-115,dz:164}
execute if score #cur rpg_tw matches 15 run function rpg:town/job/camp_at {dx:-26,dz:-198}
execute if score #cur rpg_tw matches 16 run function rpg:town/job/camp_at {dx:153,dz:129}
execute if score #cur rpg_tw matches 17 run function rpg:town/job/camp_at {dx:-200,dz:9}
execute if score #cur rpg_tw matches 18 run function rpg:town/job/camp_at {dx:141,dz:-141}
execute if score #cur rpg_tw matches 19 run function rpg:town/job/camp_at {dx:-9,dz:200}
execute if score #cur rpg_tw matches 20 run function rpg:town/job/camp_at {dx:-129,dz:-153}
execute if score #cur rpg_tw matches 21 run return run function rpg:town/job/done
execute if score #cur rpg_tw matches 21 run function rpg:town/job/camp_at {dx:198,dz:26}
execute if score #cur rpg_tw matches 22 run return run function rpg:town/job/done
execute if score #cur rpg_tw matches 22 run function rpg:town/job/camp_at {dx:-164,dz:115}
execute if score #cur rpg_tw matches 23 run return run function rpg:town/job/done
execute if score #cur rpg_tw matches 23 run function rpg:town/job/camp_at {dx:43,dz:-195}
execute if score #cur rpg_tw matches 24 run return run function rpg:town/job/done
execute if score #cur rpg_tw matches 24 run function rpg:town/job/camp_at {dx:100,dz:173}
function rpg:town/job/coords
function rpg:town/job/fl_add with storage rpg:town m
scoreboard players set #wt rpg_tw 0
scoreboard players set #ph rpg_tw 3
