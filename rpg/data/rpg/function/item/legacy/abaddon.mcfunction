# 亚巴顿 · 收割：一次明确归属的灵魂创伤，闸门阻断追加伤害递归。
scoreboard players set @s rpg_leg_cd 8
execute at @e[tag=rpg.legacy.target,limit=1] run particle minecraft:sculk_soul ~ ~1 ~ 0.45 0.65 0.45 0.04 24 force
execute at @e[tag=rpg.legacy.target,limit=1] run particle minecraft:trial_spawner_detection_ominous ~ ~1 ~ 0.35 0.5 0.35 0.05 12 force
execute as @e[tag=rpg.legacy.target,limit=1] run effect give @s minecraft:wither 4 1 true
damage @e[tag=rpg.legacy.target,limit=1] 4 minecraft:magic by @s
playsound minecraft:block.sculk_catalyst.bloom player @s ~ ~ ~ 0.8 0.55
function rpg:hud/m3
