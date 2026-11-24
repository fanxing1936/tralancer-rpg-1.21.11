# 每秒（as/at 走完新手的玩家）
execute if items entity @s container.* *[minecraft:custom_data~{rpg_sigil:1}] unless items entity @s container.* *[minecraft:custom_data~{rpg_sigil:1},minecraft:item_model="rpg:force/holy_sigil",minecraft:custom_name] run function rpg:force/x/mig/1
execute if items entity @s weapon.offhand *[minecraft:custom_data~{rpg_sigil:1}] unless items entity @s weapon.offhand *[minecraft:custom_data~{rpg_sigil:1},minecraft:item_model="rpg:force/holy_sigil",minecraft:custom_name] run function rpg:force/x/mig/1
execute if items entity @s container.* *[minecraft:custom_data~{rpg_sigil:2}] unless items entity @s container.* *[minecraft:custom_data~{rpg_sigil:2},minecraft:item_model="rpg:force/sin_sigil",minecraft:custom_name] run function rpg:force/x/mig/2
execute if items entity @s weapon.offhand *[minecraft:custom_data~{rpg_sigil:2}] unless items entity @s weapon.offhand *[minecraft:custom_data~{rpg_sigil:2},minecraft:item_model="rpg:force/sin_sigil",minecraft:custom_name] run function rpg:force/x/mig/2
tag @s remove rpg.fo.msh
execute if score @s rpg_messiah matches 1 run tag @s add rpg.fo.msh
# 王冠终式
execute if score @s rpg_sef matches 10 if score @s rpg_force matches 1 unless score @s rpg_k25 matches 1.. run function rpg:force/x/f/unlock_h
execute if score @s rpg_sef matches 10 if score @s rpg_force matches 3 unless score @s rpg_k25 matches 1.. run function rpg:force/x/f/unlock_h
execute if score @s rpg_sef matches 10 if score @s rpg_force matches 2..3 unless score @s rpg_k26 matches 1.. run function rpg:force/x/f/unlock_m
execute if score @s rpg_fo_cr > #now rpg_fo run function rpg:force/x/l/credo_sec
# 倒下：60 秒内能被圣灵复活
execute if score @s rpg_fo_die matches 1.. run function rpg:force/x/id/died
execute if entity @s[tag=rpg.fo.down] if score @s rpg_fo_dn <= #now rpg_fo run tag @s remove rpg.fo.down
execute if score @s rpg_ident matches 1 run function rpg:force/x/id/s1
execute if score @s rpg_ident matches 2 run function rpg:force/x/id/s2
execute if score @s rpg_ident matches 4 run function rpg:force/x/id/s4
execute if score @s rpg_ident matches 6 run function rpg:force/x/id/s6
