# 变身演出（as/at 载体，约 6 秒）：跪下祈祷，火刑柱升起，火爬上身体，大卫的幽灵出现，他在火里站起
scoreboard players add @s rpg_jq_c 1
execute if score @s rpg_jq_c matches 2 run function rpg:jacques_boss/morph/stake
execute if score @s rpg_jq_c matches 20..40 run particle minecraft:flame ~ ~0.3 ~ 0.4 0.2 0.4 0.02 4
execute if score @s rpg_jq_c matches 40..60 run particle minecraft:flame ~ ~1.1 ~ 0.4 0.4 0.4 0.02 5
execute if score @s rpg_jq_c matches 60..90 run particle minecraft:flame ~ ~1.9 ~ 0.4 0.5 0.4 0.03 6
execute if score @s rpg_jq_c matches 20..90 run particle minecraft:smoke ~ ~2.4 ~ 0.3 0.4 0.3 0.02 2
execute if score @s rpg_jq_c matches 20..118 run function rpg:jacques_boss/morph/ring
execute if score @s rpg_jq_c matches 44..86 run function rpg:jacques_boss/morph/helix
execute if score @s rpg_jq_c matches 60..86 run particle minecraft:dust_color_transition{from_color:[1.0,0.62,0.2],to_color:[0.35,0.04,0.0],scale:1.4} ~ ~1.2 ~ 0.5 0.9 0.5 0 3
execute if score @s rpg_jq_c matches 70..86 run particle minecraft:lava ~ ~0.5 ~ 0.5 0.2 0.5 0 1
execute if score @s rpg_jq_c matches 86..118 run particle minecraft:flame ~ ~1.2 ~ 0.4 0.8 0.4 0.03 6
execute if score @s rpg_jq_c matches 86..118 run particle minecraft:campfire_cosy_smoke ~ ~2.6 ~ 0.3 0.2 0.3 0.01 1
execute if score @s rpg_jq_c matches 20 run playsound minecraft:block.fire.ambient hostile @a[distance=..32] ~ ~ ~ 2 0.7
execute if score @s rpg_jq_c matches 50 run playsound minecraft:item.firecharge.use hostile @a[distance=..32] ~ ~ ~ 1.2 0.6
execute if score @s rpg_jq_c matches 40 run function rpg:jacques/anim/enter/kneel
execute if score @s rpg_jq_c matches 30 run function rpg:jacques_boss/morph/david
execute if score @s rpg_jq_c matches 80 run function rpg:jacques/anim/enter/hero
execute if score @s rpg_jq_c matches 86 run function rpg:jacques_boss/morph/rise
execute if score @s rpg_jq_c matches 120.. run function rpg:jacques_boss/stage/begin2
