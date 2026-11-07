# 已有柱位。手里必须是**自己那一本已立约的书** —— 攥着别柱的书没有用。
execute unless entity @s[tag=rpg.pact.off] unless items entity @s weapon.mainhand *[minecraft:custom_data~{pact_signed:1b}] run return run function rpg:pact/reissue
execute if entity @s[tag=rpg.pact.off] unless items entity @s weapon.offhand *[minecraft:custom_data~{pact_signed:1b}] run return run function rpg:pact/reissue

# 旧存档的立约者没有阶位；书的阶位落后时就地换新，不必等下一次升阶。
execute unless score @s rpg_pact_lv matches 1.. run function rpg:pact/oath/migrate
function rpg:pact/book/stale

# 站在一支**燃着的**驱魔图腾旁边举起这本书，不是动用力量，而是毁约。
# 这是逆圣化之外的第二条解约途径 —— 详见 rpg:pact/renounce。
execute if entity @e[type=minecraft:item_display,tag=rpg.totem.lit,distance=..6] run return run function rpg:pact/renounce

# 四种长按：普通放力量，潜行放二阶技能，潜行抬头化身，潜行低头打开契约。
execute if predicate rpg:sneaking if entity @s[x_rotation=45..90] run return run function rpg:pact/ui/open
execute if predicate rpg:sneaking if entity @s[x_rotation=-90..-45] run return run function rpg:pact/depth/avatar
execute if predicate rpg:sneaking run return run function rpg:pact/depth/second

execute if entity @s[scores={rpg_pact_cd=1..}] run return run function rpg:pact/cooling

scoreboard players set @s rpg_pact_cd 300
scoreboard players add @s rpg_taint 3
tag @s add rpg.pact.cast
execute if entity @s[scores={rpg_pact=1}] run function rpg:pact/p1
execute if entity @s[scores={rpg_pact=2}] run function rpg:pact/p2
execute if entity @s[scores={rpg_pact=3}] run function rpg:pact/p3
execute if entity @s[scores={rpg_pact=4}] run function rpg:pact/p4
execute if entity @s[scores={rpg_pact=5}] run function rpg:pact/p5
execute if entity @s[scores={rpg_pact=6}] run function rpg:pact/p6
execute if entity @s[scores={rpg_pact=7}] run function rpg:pact/p7
tag @s remove rpg.pact.cast
