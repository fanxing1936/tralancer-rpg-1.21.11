# 每两秒（as/at 玩家）：算综合能力，够了就晋阶。新手开局没走完的人还没入王国。
execute unless score @s rpg_ob_v matches 1.. run return 0
execute unless score @s rpg_ob matches 100 run return 0
scoreboard players add @s rpg_ex_xp 0
scoreboard players set #g rpg_sef 0
execute if items entity @s armor.head *[minecraft:custom_data~{rpg_eq:{lv:1}}] run scoreboard players add #g rpg_sef 2
execute if items entity @s armor.head *[minecraft:custom_data~{rpg_eq:{lv:2}}] run scoreboard players add #g rpg_sef 4
execute if items entity @s armor.head *[minecraft:custom_data~{rpg_eq:{lv:3}}] run scoreboard players add #g rpg_sef 8
execute if items entity @s armor.head *[minecraft:custom_data~{rpg_eq:{lv:4}}] run scoreboard players add #g rpg_sef 16
execute if items entity @s armor.head *[minecraft:custom_data~{rpg_eq:{lv:5}}] run scoreboard players add #g rpg_sef 32
execute if items entity @s armor.head *[minecraft:custom_data~{rpg_eq:{lv:6}}] run scoreboard players add #g rpg_sef 64
execute if items entity @s armor.head *[minecraft:custom_data~{rpg_eq:{lv:7}}] run scoreboard players add #g rpg_sef 128
execute if items entity @s armor.head *[minecraft:custom_data~{rpg_eq:{lv:8}}] run scoreboard players add #g rpg_sef 256
execute if items entity @s armor.head *[minecraft:custom_data~{rpg_eq:{lv:9}}] run scoreboard players add #g rpg_sef 512
execute if items entity @s armor.head *[minecraft:custom_data~{rpg_eq:{lv:10}}] run scoreboard players add #g rpg_sef 1024
execute if items entity @s armor.chest *[minecraft:custom_data~{rpg_eq:{lv:1}}] run scoreboard players add #g rpg_sef 2
execute if items entity @s armor.chest *[minecraft:custom_data~{rpg_eq:{lv:2}}] run scoreboard players add #g rpg_sef 4
execute if items entity @s armor.chest *[minecraft:custom_data~{rpg_eq:{lv:3}}] run scoreboard players add #g rpg_sef 8
execute if items entity @s armor.chest *[minecraft:custom_data~{rpg_eq:{lv:4}}] run scoreboard players add #g rpg_sef 16
execute if items entity @s armor.chest *[minecraft:custom_data~{rpg_eq:{lv:5}}] run scoreboard players add #g rpg_sef 32
execute if items entity @s armor.chest *[minecraft:custom_data~{rpg_eq:{lv:6}}] run scoreboard players add #g rpg_sef 64
execute if items entity @s armor.chest *[minecraft:custom_data~{rpg_eq:{lv:7}}] run scoreboard players add #g rpg_sef 128
execute if items entity @s armor.chest *[minecraft:custom_data~{rpg_eq:{lv:8}}] run scoreboard players add #g rpg_sef 256
execute if items entity @s armor.chest *[minecraft:custom_data~{rpg_eq:{lv:9}}] run scoreboard players add #g rpg_sef 512
execute if items entity @s armor.chest *[minecraft:custom_data~{rpg_eq:{lv:10}}] run scoreboard players add #g rpg_sef 1024
execute if items entity @s armor.legs *[minecraft:custom_data~{rpg_eq:{lv:1}}] run scoreboard players add #g rpg_sef 2
execute if items entity @s armor.legs *[minecraft:custom_data~{rpg_eq:{lv:2}}] run scoreboard players add #g rpg_sef 4
execute if items entity @s armor.legs *[minecraft:custom_data~{rpg_eq:{lv:3}}] run scoreboard players add #g rpg_sef 8
execute if items entity @s armor.legs *[minecraft:custom_data~{rpg_eq:{lv:4}}] run scoreboard players add #g rpg_sef 16
execute if items entity @s armor.legs *[minecraft:custom_data~{rpg_eq:{lv:5}}] run scoreboard players add #g rpg_sef 32
execute if items entity @s armor.legs *[minecraft:custom_data~{rpg_eq:{lv:6}}] run scoreboard players add #g rpg_sef 64
execute if items entity @s armor.legs *[minecraft:custom_data~{rpg_eq:{lv:7}}] run scoreboard players add #g rpg_sef 128
execute if items entity @s armor.legs *[minecraft:custom_data~{rpg_eq:{lv:8}}] run scoreboard players add #g rpg_sef 256
execute if items entity @s armor.legs *[minecraft:custom_data~{rpg_eq:{lv:9}}] run scoreboard players add #g rpg_sef 512
execute if items entity @s armor.legs *[minecraft:custom_data~{rpg_eq:{lv:10}}] run scoreboard players add #g rpg_sef 1024
execute if items entity @s armor.feet *[minecraft:custom_data~{rpg_eq:{lv:1}}] run scoreboard players add #g rpg_sef 2
execute if items entity @s armor.feet *[minecraft:custom_data~{rpg_eq:{lv:2}}] run scoreboard players add #g rpg_sef 4
execute if items entity @s armor.feet *[minecraft:custom_data~{rpg_eq:{lv:3}}] run scoreboard players add #g rpg_sef 8
execute if items entity @s armor.feet *[minecraft:custom_data~{rpg_eq:{lv:4}}] run scoreboard players add #g rpg_sef 16
execute if items entity @s armor.feet *[minecraft:custom_data~{rpg_eq:{lv:5}}] run scoreboard players add #g rpg_sef 32
execute if items entity @s armor.feet *[minecraft:custom_data~{rpg_eq:{lv:6}}] run scoreboard players add #g rpg_sef 64
execute if items entity @s armor.feet *[minecraft:custom_data~{rpg_eq:{lv:7}}] run scoreboard players add #g rpg_sef 128
execute if items entity @s armor.feet *[minecraft:custom_data~{rpg_eq:{lv:8}}] run scoreboard players add #g rpg_sef 256
execute if items entity @s armor.feet *[minecraft:custom_data~{rpg_eq:{lv:9}}] run scoreboard players add #g rpg_sef 512
execute if items entity @s armor.feet *[minecraft:custom_data~{rpg_eq:{lv:10}}] run scoreboard players add #g rpg_sef 1024
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_eq:{lv:1}}] run scoreboard players add #g rpg_sef 2
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_eq:{lv:2}}] run scoreboard players add #g rpg_sef 4
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_eq:{lv:3}}] run scoreboard players add #g rpg_sef 8
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_eq:{lv:4}}] run scoreboard players add #g rpg_sef 16
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_eq:{lv:5}}] run scoreboard players add #g rpg_sef 32
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_eq:{lv:6}}] run scoreboard players add #g rpg_sef 64
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_eq:{lv:7}}] run scoreboard players add #g rpg_sef 128
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_eq:{lv:8}}] run scoreboard players add #g rpg_sef 256
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_eq:{lv:9}}] run scoreboard players add #g rpg_sef 512
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_eq:{lv:10}}] run scoreboard players add #g rpg_sef 1024
scoreboard players operation @s rpg_gear = #g rpg_sef
scoreboard players operation @s rpg_power = @s rpg_ex_xp
scoreboard players operation @s rpg_power += @s rpg_gear
function rpg:paths/check
execute unless score @s rpg_sef matches 1.. run function rpg:sephira/tier/up_1
execute if score @s rpg_sef matches 1 if score @s rpg_power matches 60.. run function rpg:sephira/tier/up_2
execute if score @s rpg_sef matches 2 if score @s rpg_ps_32 matches 2.. if score @s rpg_power matches 180.. run function rpg:sephira/tier/up_3
execute if score @s rpg_sef matches 3 if score @s rpg_ps_31 matches 2.. if score @s rpg_power matches 420.. run function rpg:sephira/tier/up_4
execute if score @s rpg_sef matches 3 if score @s rpg_ps_30 matches 2.. if score @s rpg_power matches 420.. run function rpg:sephira/tier/up_4
execute if score @s rpg_sef matches 4 if score @s rpg_ps_29 matches 2.. if score @s rpg_power matches 900.. run function rpg:sephira/tier/up_5
execute if score @s rpg_sef matches 4 if score @s rpg_ps_28 matches 2.. if score @s rpg_power matches 900.. run function rpg:sephira/tier/up_5
execute if score @s rpg_sef matches 4 if score @s rpg_ps_27 matches 2.. if score @s rpg_power matches 900.. run function rpg:sephira/tier/up_5
execute if score @s rpg_sef matches 5 if score @s rpg_ps_26 matches 2.. if score @s rpg_power matches 1860.. run function rpg:sephira/tier/up_6
execute if score @s rpg_sef matches 5 if score @s rpg_ps_25 matches 2.. if score @s rpg_power matches 1860.. run function rpg:sephira/tier/up_6
execute if score @s rpg_sef matches 5 if score @s rpg_ps_24 matches 2.. if score @s rpg_power matches 1860.. run function rpg:sephira/tier/up_6
execute if score @s rpg_sef matches 6 if score @s rpg_ps_23 matches 2.. if score @s rpg_power matches 3780.. run function rpg:sephira/tier/up_7
execute if score @s rpg_sef matches 6 if score @s rpg_ps_22 matches 2.. if score @s rpg_power matches 3780.. run function rpg:sephira/tier/up_7
execute if score @s rpg_sef matches 7 unless score @s rpg_daath matches 1 run function rpg:sephira/daath/start
execute if score @s rpg_sef matches 7 if score @s rpg_ps_21 matches 2.. if score @s rpg_daath matches 1 if score @s rpg_power matches 7620.. run function rpg:sephira/tier/up_8
execute if score @s rpg_sef matches 7 if score @s rpg_ps_20 matches 2.. if score @s rpg_daath matches 1 if score @s rpg_power matches 7620.. run function rpg:sephira/tier/up_8
execute if score @s rpg_sef matches 7 if score @s rpg_ps_19 matches 2.. if score @s rpg_daath matches 1 if score @s rpg_power matches 7620.. run function rpg:sephira/tier/up_8
execute if score @s rpg_sef matches 8 if score @s rpg_ps_18 matches 2.. if score @s rpg_power matches 15300.. run function rpg:sephira/tier/up_9
execute if score @s rpg_sef matches 8 if score @s rpg_ps_17 matches 2.. if score @s rpg_power matches 15300.. run function rpg:sephira/tier/up_9
execute if score @s rpg_sef matches 9 if score @s rpg_ps_16 matches 2.. if score @s rpg_power matches 30660.. run function rpg:sephira/tier/up_10
execute if score @s rpg_sef matches 9 if score @s rpg_ps_15 matches 2.. if score @s rpg_power matches 30660.. run function rpg:sephira/tier/up_10
execute if score @s rpg_sef matches 9 if score @s rpg_ps_14 matches 2.. if score @s rpg_power matches 30660.. run function rpg:sephira/tier/up_10
execute if score @s rpg_sef matches 2 if score @s rpg_power matches 180.. unless score @s rpg_pa_wt matches 2 run function rpg:paths/wait
execute if score @s rpg_sef matches 3 if score @s rpg_power matches 420.. unless score @s rpg_pa_wt matches 3 run function rpg:paths/wait
execute if score @s rpg_sef matches 4 if score @s rpg_power matches 900.. unless score @s rpg_pa_wt matches 4 run function rpg:paths/wait
execute if score @s rpg_sef matches 5 if score @s rpg_power matches 1860.. unless score @s rpg_pa_wt matches 5 run function rpg:paths/wait
execute if score @s rpg_sef matches 6 if score @s rpg_power matches 3780.. unless score @s rpg_pa_wt matches 6 run function rpg:paths/wait
execute if score @s rpg_sef matches 7 if score @s rpg_daath matches 1 if score @s rpg_power matches 7620.. unless score @s rpg_pa_wt matches 7 run function rpg:paths/wait
execute if score @s rpg_sef matches 8 if score @s rpg_power matches 15300.. unless score @s rpg_pa_wt matches 8 run function rpg:paths/wait
execute if score @s rpg_sef matches 9 if score @s rpg_power matches 30660.. unless score @s rpg_pa_wt matches 9 run function rpg:paths/wait
