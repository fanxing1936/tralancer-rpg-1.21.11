# 阵营（add_pvp.py）：同阵营、安全区里的玩家不吃额外伤害
execute if entity @s[type=minecraft:player,tag=rpg.safe] run return 0
execute if entity @s[type=minecraft:player,tag=rpg.ch] if entity @a[tag=rpg.fg.atk,tag=rpg.ch] run return 0
execute if entity @s[type=minecraft:player,tag=rpg.dm] if entity @a[tag=rpg.fg.atk,tag=rpg.dm] run return 0
scoreboard players set #mel rpg_fg 0
scoreboard players set #rng rpg_fg 0
execute if entity @a[tag=rpg.fg.atk,scores={rpg_fg_dd=1..}] run scoreboard players set #mel rpg_fg 1
execute if score #mel rpg_fg matches 0 if entity @a[tag=rpg.fg.atk,tag=rpg.fg.k.ranged,scores={rpg_fg_shot=1..},distance=3..] if entity @s[nbt={HurtTime:10s}] run scoreboard players set #rng rpg_fg 1
execute if score #mel rpg_fg matches 0 if score #rng rpg_fg matches 0 run return 0
scoreboard players set #pct rpg_fg 0
scoreboard players set #spct rpg_fg 0
# 六源
scoreboard players set #fa rpg_fg 0
execute if entity @s[type=#minecraft:undead] run scoreboard players set #fa rpg_fg 1
execute if entity @s[tag=rpg.demon] run scoreboard players set #fa rpg_fg 1
execute if entity @s[tag=rpg.demon.minion] run scoreboard players set #fa rpg_fg 1
execute if score #fa rpg_fg matches 1 if entity @a[tag=rpg.fg.atk,tag=rpg.fg.src.faith] run scoreboard players add #spct rpg_fg 25
execute if entity @a[tag=rpg.fg.atk,tag=rpg.fg.src.malice] run scoreboard players add #spct rpg_fg 15
execute as @a[tag=rpg.fg.atk,tag=rpg.fg.src.pride] run function rpg:forge/src/pride_check
execute if entity @a[tag=rpg.fg.atk,tag=rpg.fg.src.resolve,scores={rpg_fg_rs=1..}] run scoreboard players add #spct rpg_fg 30
scoreboard players set @a[tag=rpg.fg.atk,tag=rpg.fg.src.resolve] rpg_fg_rs 0
execute if entity @a[tag=rpg.fg.atk,tag=rpg.fg.src.hatred] run function rpg:forge/src/hatred
execute if entity @a[tag=rpg.fg.atk,tag=rpg.fg.lv10] run scoreboard players operation #spct rpg_fg *= #3 rpg_fg
execute if entity @a[tag=rpg.fg.atk,tag=rpg.fg.lv10] run scoreboard players operation #spct rpg_fg /= #2 rpg_fg
scoreboard players operation #pct rpg_fg += #spct rpg_fg
# 符文与窗口
execute if score #mel rpg_fg matches 1 run function rpg:forge/hit/melee
execute if score #rng rpg_fg matches 1 run function rpg:forge/hit/ranged
execute if entity @a[tag=rpg.fg.atk,scores={rpg_fg_bl=1..}] run function rpg:forge/stone/blood_leech
# 符石能量
execute if score #mel rpg_fg matches 1 as @a[tag=rpg.fg.atk,tag=rpg.fg.st] run scoreboard players add @s rpg_fg_en 8
execute if score #rng rpg_fg matches 1 as @a[tag=rpg.fg.atk,tag=rpg.fg.st] run scoreboard players add @s rpg_fg_en 12
scoreboard players set @a[tag=rpg.fg.atk,scores={rpg_fg_en=101..}] rpg_fg_en 100
execute if score #pct rpg_fg matches 1.. run function rpg:forge/hit/bonus
