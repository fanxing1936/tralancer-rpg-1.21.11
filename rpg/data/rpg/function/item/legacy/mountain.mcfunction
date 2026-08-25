# 高山之啸 · 怒嚎：厚重、低频的震裂，而非旧版无差别最近实体 1 点伤害。
scoreboard players set @s rpg_leg_cd 12
execute at @e[tag=rpg.legacy.target,limit=1] run particle minecraft:block{block_state:{Name:"minecraft:tuff"}} ~ ~0.8 ~ 0.6 0.35 0.6 0.12 32 force
execute at @e[tag=rpg.legacy.target,limit=1] run particle minecraft:gust ~ ~1 ~ 0.35 0.25 0.35 0.08 8 force
execute as @e[tag=rpg.legacy.target,limit=1] run effect give @s minecraft:slowness 2 1 true
damage @e[tag=rpg.legacy.target,limit=1] 4 minecraft:sonic_boom by @s
playsound minecraft:item.mace.smash_ground player @s ~ ~ ~ 0.8 0.75
function rpg:hud/m7
