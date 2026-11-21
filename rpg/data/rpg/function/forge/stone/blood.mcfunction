execute store result score #t rpg_fg run data get entity @s Health
scoreboard players operation #t rpg_fg /= #5 rpg_fg
execute if score #t rpg_fg matches ..0 run scoreboard players set #t rpg_fg 1
execute store result storage rpg:forge dmg.n int 1 run scoreboard players get #t rpg_fg
function rpg:forge/src/self_dmg with storage rpg:forge dmg
scoreboard players set @s rpg_fg_bl 160
scoreboard players set @s rpg_fg_blh 0
particle minecraft:damage_indicator ~ ~1 ~ 0.4 0.6 0.4 0.1 16
playsound minecraft:entity.warden.heartbeat player @a[distance=..16] ~ ~ ~ 1 1.2
