function rpg:sephira/kill
scoreboard players operation #xa rpg_fg = @s rpg_fg_kx
execute if score @s rpg_ps_15 matches 2 if predicate {condition:"minecraft:random_chance",chance:0.2} run scoreboard players operation #xa rpg_fg += #xa rpg_fg
scoreboard players reset @s rpg_fg_kx
execute if entity @s[tag=rpg.fg.src.hope] run function rpg:forge/src/hope
execute if entity @s[tag=rpg.fg.a.swift] run effect give @s minecraft:speed 3 1 true
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_eq:{}}] run function rpg:forge/xp/main
scoreboard players set #xa rpg_fg 1
execute if items entity @s armor.head *[minecraft:custom_data~{rpg_eq:{}}] run function rpg:forge/xp/head
execute if items entity @s armor.chest *[minecraft:custom_data~{rpg_eq:{}}] run function rpg:forge/xp/chest
execute if items entity @s armor.legs *[minecraft:custom_data~{rpg_eq:{}}] run function rpg:forge/xp/legs
execute if items entity @s armor.feet *[minecraft:custom_data~{rpg_eq:{}}] run function rpg:forge/xp/feet
execute if score @s rpg_ident matches 4 if score @s rpg_ident_sin matches 7 run function rpg:force/x/id/greed
