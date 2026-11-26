# 右键了营火上的交互实体（as 玩家）：空手开工作台；万一手里刚换上东西，交给原来的材料右键
advancement revoke @s only rpg:bench/use
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_fm:1b}] run return run function rpg:forge/use
execute if items entity @s weapon.mainhand * run return 0
execute if entity @s[tag=rpg.fg.ui] run return 0
tag @s add rpg.fg.ui
scoreboard players set @s rpg_fg_lk 6
function rpg:bench/home
