# 每两秒（as/at 玩家）：算综合能力，够了就晋阶。新手开局没走完的人还没入王国。
execute unless score @s rpg_ob_v matches 1.. run return 0
execute unless score @s rpg_ob matches 100 run return 0
scoreboard players add @s rpg_ex_xp 0
scoreboard players set #g rpg_sef 0
execute if items entity @s armor.head *[minecraft:custom_data~{rpg_eq:{lv:1}}] run scoreboard players add #g rpg_sef 1
execute if items entity @s armor.head *[minecraft:custom_data~{rpg_eq:{lv:2}}] run scoreboard players add #g rpg_sef 2
execute if items entity @s armor.head *[minecraft:custom_data~{rpg_eq:{lv:3}}] run scoreboard players add #g rpg_sef 3
execute if items entity @s armor.head *[minecraft:custom_data~{rpg_eq:{lv:4}}] run scoreboard players add #g rpg_sef 4
execute if items entity @s armor.head *[minecraft:custom_data~{rpg_eq:{lv:5}}] run scoreboard players add #g rpg_sef 5
execute if items entity @s armor.head *[minecraft:custom_data~{rpg_eq:{lv:6}}] run scoreboard players add #g rpg_sef 6
execute if items entity @s armor.head *[minecraft:custom_data~{rpg_eq:{lv:7}}] run scoreboard players add #g rpg_sef 7
execute if items entity @s armor.head *[minecraft:custom_data~{rpg_eq:{lv:8}}] run scoreboard players add #g rpg_sef 8
execute if items entity @s armor.head *[minecraft:custom_data~{rpg_eq:{lv:9}}] run scoreboard players add #g rpg_sef 9
execute if items entity @s armor.head *[minecraft:custom_data~{rpg_eq:{lv:10}}] run scoreboard players add #g rpg_sef 10
execute if items entity @s armor.chest *[minecraft:custom_data~{rpg_eq:{lv:1}}] run scoreboard players add #g rpg_sef 1
execute if items entity @s armor.chest *[minecraft:custom_data~{rpg_eq:{lv:2}}] run scoreboard players add #g rpg_sef 2
execute if items entity @s armor.chest *[minecraft:custom_data~{rpg_eq:{lv:3}}] run scoreboard players add #g rpg_sef 3
execute if items entity @s armor.chest *[minecraft:custom_data~{rpg_eq:{lv:4}}] run scoreboard players add #g rpg_sef 4
execute if items entity @s armor.chest *[minecraft:custom_data~{rpg_eq:{lv:5}}] run scoreboard players add #g rpg_sef 5
execute if items entity @s armor.chest *[minecraft:custom_data~{rpg_eq:{lv:6}}] run scoreboard players add #g rpg_sef 6
execute if items entity @s armor.chest *[minecraft:custom_data~{rpg_eq:{lv:7}}] run scoreboard players add #g rpg_sef 7
execute if items entity @s armor.chest *[minecraft:custom_data~{rpg_eq:{lv:8}}] run scoreboard players add #g rpg_sef 8
execute if items entity @s armor.chest *[minecraft:custom_data~{rpg_eq:{lv:9}}] run scoreboard players add #g rpg_sef 9
execute if items entity @s armor.chest *[minecraft:custom_data~{rpg_eq:{lv:10}}] run scoreboard players add #g rpg_sef 10
execute if items entity @s armor.legs *[minecraft:custom_data~{rpg_eq:{lv:1}}] run scoreboard players add #g rpg_sef 1
execute if items entity @s armor.legs *[minecraft:custom_data~{rpg_eq:{lv:2}}] run scoreboard players add #g rpg_sef 2
execute if items entity @s armor.legs *[minecraft:custom_data~{rpg_eq:{lv:3}}] run scoreboard players add #g rpg_sef 3
execute if items entity @s armor.legs *[minecraft:custom_data~{rpg_eq:{lv:4}}] run scoreboard players add #g rpg_sef 4
execute if items entity @s armor.legs *[minecraft:custom_data~{rpg_eq:{lv:5}}] run scoreboard players add #g rpg_sef 5
execute if items entity @s armor.legs *[minecraft:custom_data~{rpg_eq:{lv:6}}] run scoreboard players add #g rpg_sef 6
execute if items entity @s armor.legs *[minecraft:custom_data~{rpg_eq:{lv:7}}] run scoreboard players add #g rpg_sef 7
execute if items entity @s armor.legs *[minecraft:custom_data~{rpg_eq:{lv:8}}] run scoreboard players add #g rpg_sef 8
execute if items entity @s armor.legs *[minecraft:custom_data~{rpg_eq:{lv:9}}] run scoreboard players add #g rpg_sef 9
execute if items entity @s armor.legs *[minecraft:custom_data~{rpg_eq:{lv:10}}] run scoreboard players add #g rpg_sef 10
execute if items entity @s armor.feet *[minecraft:custom_data~{rpg_eq:{lv:1}}] run scoreboard players add #g rpg_sef 1
execute if items entity @s armor.feet *[minecraft:custom_data~{rpg_eq:{lv:2}}] run scoreboard players add #g rpg_sef 2
execute if items entity @s armor.feet *[minecraft:custom_data~{rpg_eq:{lv:3}}] run scoreboard players add #g rpg_sef 3
execute if items entity @s armor.feet *[minecraft:custom_data~{rpg_eq:{lv:4}}] run scoreboard players add #g rpg_sef 4
execute if items entity @s armor.feet *[minecraft:custom_data~{rpg_eq:{lv:5}}] run scoreboard players add #g rpg_sef 5
execute if items entity @s armor.feet *[minecraft:custom_data~{rpg_eq:{lv:6}}] run scoreboard players add #g rpg_sef 6
execute if items entity @s armor.feet *[minecraft:custom_data~{rpg_eq:{lv:7}}] run scoreboard players add #g rpg_sef 7
execute if items entity @s armor.feet *[minecraft:custom_data~{rpg_eq:{lv:8}}] run scoreboard players add #g rpg_sef 8
execute if items entity @s armor.feet *[minecraft:custom_data~{rpg_eq:{lv:9}}] run scoreboard players add #g rpg_sef 9
execute if items entity @s armor.feet *[minecraft:custom_data~{rpg_eq:{lv:10}}] run scoreboard players add #g rpg_sef 10
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_eq:{lv:1}}] run scoreboard players add #g rpg_sef 1
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_eq:{lv:2}}] run scoreboard players add #g rpg_sef 2
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_eq:{lv:3}}] run scoreboard players add #g rpg_sef 3
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_eq:{lv:4}}] run scoreboard players add #g rpg_sef 4
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_eq:{lv:5}}] run scoreboard players add #g rpg_sef 5
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_eq:{lv:6}}] run scoreboard players add #g rpg_sef 6
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_eq:{lv:7}}] run scoreboard players add #g rpg_sef 7
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_eq:{lv:8}}] run scoreboard players add #g rpg_sef 8
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_eq:{lv:9}}] run scoreboard players add #g rpg_sef 9
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_eq:{lv:10}}] run scoreboard players add #g rpg_sef 10
scoreboard players operation @s rpg_gear = #g rpg_sef
scoreboard players operation @s rpg_gear *= #10 rpg_sef
scoreboard players operation @s rpg_power = @s rpg_ex_xp
scoreboard players operation @s rpg_power += @s rpg_gear
execute unless score @s rpg_sef matches 1.. run function rpg:sephira/tier/up_1
execute if score @s rpg_sef matches 1 if score @s rpg_power matches 60.. run function rpg:sephira/tier/up_2
execute if score @s rpg_sef matches 2 if score @s rpg_power matches 160.. run function rpg:sephira/tier/up_3
execute if score @s rpg_sef matches 3 if score @s rpg_power matches 300.. run function rpg:sephira/tier/up_4
execute if score @s rpg_sef matches 4 if score @s rpg_power matches 480.. run function rpg:sephira/tier/up_5
execute if score @s rpg_sef matches 5 if score @s rpg_power matches 700.. run function rpg:sephira/tier/up_6
execute if score @s rpg_sef matches 6 if score @s rpg_power matches 950.. run function rpg:sephira/tier/up_7
execute if score @s rpg_sef matches 7 unless score @s rpg_daath matches 1 run function rpg:sephira/daath/start
execute if score @s rpg_sef matches 7 if score @s rpg_daath matches 1 if score @s rpg_power matches 1250.. run function rpg:sephira/tier/up_8
execute if score @s rpg_sef matches 8 if score @s rpg_power matches 1600.. run function rpg:sephira/tier/up_9
execute if score @s rpg_sef matches 9 if score @s rpg_power matches 2000.. run function rpg:sephira/tier/up_10
