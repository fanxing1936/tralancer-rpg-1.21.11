# 圣徽 / 罪印被按下（rpg:force/use 进度，按住期间每刻都响：只认按下的那一刻）
advancement revoke @s only rpg:force/use
execute store result score #now rpg_fo run time query gametime
scoreboard players operation #g rpg_fo = #now rpg_fo
scoreboard players remove #g rpg_fo 1
execute if score @s rpg_fo_last >= #g rpg_fo run return run scoreboard players operation @s rpg_fo_last = #now rpg_fo
scoreboard players operation @s rpg_fo_last = #now rpg_fo
scoreboard players set #tree rpg_fo 0
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_sigil:1}] run scoreboard players set #tree rpg_fo 1
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_sigil:2}] run scoreboard players set #tree rpg_fo 2
execute if score #tree rpg_fo matches 0 if items entity @s weapon.offhand *[minecraft:custom_data~{rpg_sigil:1}] run scoreboard players set #tree rpg_fo 1
execute if score #tree rpg_fo matches 0 if items entity @s weapon.offhand *[minecraft:custom_data~{rpg_sigil:2}] run scoreboard players set #tree rpg_fo 2
execute if score #tree rpg_fo matches 0 run return 0
scoreboard players set #slot rpg_fo 1
execute if predicate rpg:sneaking run scoreboard players set #slot rpg_fo 2
function rpg:force/cast
