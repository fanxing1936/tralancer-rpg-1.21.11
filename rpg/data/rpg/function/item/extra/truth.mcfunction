# 求真之刃［洞悉］
# 命中即显形；当目标生命值降到 20 以下，谎言散尽，追加一次真实伤害。
# 血量直接读 damage_action —— 那是 rpg:command/index 每刻已经抓好的，不额外开销。
execute if entity @e[tag=rpg.hurt] run function rpg:item/extra/truth/g0
execute as @e[tag=rpg.hurt,scores={damage_action=..20}] at @s if entity @a[tag=rpg.truth.src,distance=..7] run particle enchanted_hit ~ ~1 ~ 0.3 0.4 0.3 0 20
execute as @e[tag=rpg.hurt,scores={damage_action=..20}] at @s if entity @a[tag=rpg.truth.src,distance=..7] run particle dust_color_transition{from_color:[1.0,0.95,0.8],to_color:[0.8,0.1,0.1],scale:2} ~ ~1 ~ 0.4 0.5 0.4 0.1 30
execute as @e[tag=rpg.hurt,scores={damage_action=..20},type=!player] at @s if entity @a[tag=rpg.truth.src,distance=..7] run damage @s 4 minecraft:magic by @a[tag=rpg.truth.src,limit=1,sort=nearest]
execute as @e[tag=rpg.hurt,scores={damage_action=..20}] at @s if entity @a[tag=rpg.truth.src,distance=..7] run playsound minecraft:block.amethyst_block.resonate player @a[distance=..12]
tag @a[tag=rpg.truth.src] remove rpg.truth.src
scoreboard players reset * truth
