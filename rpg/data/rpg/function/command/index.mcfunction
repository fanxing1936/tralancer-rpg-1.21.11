# Auto-generated per-tick flag index.
# 每个族群只遍历一次：清标记与判定都在 @s 上完成，
# 于是玩家表每刻只走一遍、掉落物表也只走一遍。

execute as @a run function rpg:command/index_player
execute as @e[type=minecraft:item] run function rpg:command/index_item

## damage detection
tag @e[tag=rpg.hurt] remove rpg.hurt
execute as @a at @s run function rpg:command/damage_scan
execute if entity @a[tag=rpg.seal.active4,limit=1] as @e[tag=rpg.hurt,type=#rpg:seal_hostile,tag=!rpg.demon,tag=!rpg.demon.minion,nbt={Health:0.0f}] at @s run function rpg:inquest/seal/ability/beelzebub_death
execute if entity @a[tag=rpg.seal.active4,limit=1] as @e[tag=rpg.hurt,tag=rpg.demon,nbt={Health:0.0f}] at @s run function rpg:inquest/seal/ability/beelzebub_death
execute if entity @a[tag=rpg.seal.active4,limit=1] as @e[tag=rpg.hurt,tag=rpg.demon.minion,tag=!rpg.demon,nbt={Health:0.0f}] at @s run function rpg:inquest/seal/ability/beelzebub_death
