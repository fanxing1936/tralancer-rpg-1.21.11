# 藤蔓之鞭［缠绕］—— 起手看浮标，之后每刻负责落鞭。
function rpg:item/extra/vine_trigger

#
# 每鞭间隔 10 刻：生物受伤后有约 10 刻无敌帧，连着每刻打只有第一下算数。
# 计数器从 60 倒数，在 50 / 40 / 30 / 20 / 10 / 1 六个刻落鞭，正好三秒六鞭。
execute as @e[scores={rpg_vine_lash=50}] run tag @s add rpg.vine.strike
execute as @e[scores={rpg_vine_lash=40}] run tag @s add rpg.vine.strike
execute as @e[scores={rpg_vine_lash=30}] run tag @s add rpg.vine.strike
execute as @e[scores={rpg_vine_lash=20}] run tag @s add rpg.vine.strike
execute as @e[scores={rpg_vine_lash=10}] run tag @s add rpg.vine.strike
execute as @e[scores={rpg_vine_lash=1}] run tag @s add rpg.vine.strike

execute if entity @e[tag=rpg.vine.strike] run function rpg:item/extra/vine/g0

# 音调逐鞭升高，一耳就能听出打到第几鞭
execute as @e[scores={rpg_vine_lash=50}] at @s run playsound minecraft:entity.player.attack.sweep player @a[distance=..16] ~ ~ ~ 1 0.8
execute as @e[scores={rpg_vine_lash=40}] at @s run playsound minecraft:entity.player.attack.sweep player @a[distance=..16] ~ ~ ~ 1 0.95
execute as @e[scores={rpg_vine_lash=30}] at @s run playsound minecraft:entity.player.attack.sweep player @a[distance=..16] ~ ~ ~ 1 1.1
execute as @e[scores={rpg_vine_lash=20}] at @s run playsound minecraft:entity.player.attack.sweep player @a[distance=..16] ~ ~ ~ 1 1.3
execute as @e[scores={rpg_vine_lash=10}] at @s run playsound minecraft:entity.player.attack.sweep player @a[distance=..16] ~ ~ ~ 1 1.5
execute as @e[scores={rpg_vine_lash=1}] at @s run playsound minecraft:entity.player.attack.sweep player @a[distance=..16] ~ ~ ~ 1 1.8

tag @e[tag=rpg.vine.strike] remove rpg.vine.strike
execute as @e[tag=rpg.vine.lash,scores={rpg_vine_lash=1..}] run scoreboard players remove @s rpg_vine_lash 1
tag @e[tag=rpg.vine.lash,scores={rpg_vine_lash=..0}] remove rpg.vine.lash
