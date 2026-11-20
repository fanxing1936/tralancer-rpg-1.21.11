# 战场（as/at 战场中心）。
scoreboard players add #tick rpg_sl 1
execute if entity @e[tag=rpg.unit.f,distance=..40] run scoreboard players set #empty rpg_sl 0
execute unless entity @e[tag=rpg.unit.f,distance=..40] run scoreboard players add #empty rpg_sl 1
execute if score #empty rpg_sl matches 1200.. run return run function rpg:saul_boss/lose
execute unless entity @e[type=minecraft:vindicator,tag=rpg.slb,tag=!rpg.slb.preview,distance=..120] run return run function rpg:saul_boss/lost_unit
bossbar set rpg:saul_boss players @a[distance=..48]
execute as @e[type=minecraft:vindicator,tag=rpg.slb,tag=!rpg.slb.preview,distance=..120] at @s run function rpg:saul_boss/unit
execute as @e[tag=rpg.slb.fx,distance=..120] at @s run function rpg:saul_boss/fx/tick
# 上一刻被判了格挡 / 多扣的那一下：伤害统计这时才记上，按增量结算；然后所有人的统计基准对齐到这一刻
execute as @e[tag=rpg.unit,tag=rpg.slb.pend] run function rpg:saul_boss/hit/settle
execute as @e[tag=rpg.unit] run scoreboard players operation @s rpg_sl_dd0 = @s rpg_sl_dd
function rpg:saul_boss/music/tick
