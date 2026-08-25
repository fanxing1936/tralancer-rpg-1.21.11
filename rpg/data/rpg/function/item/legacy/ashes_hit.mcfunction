# 别西卜 · 普通攻击：恢复原作四段灰烬表现，但目标与攻击者都走精确归属。
# 不召唤命名盔甲架、不用 @p；五刻闸门也会拦住第四段追加伤害的递归事件。
scoreboard players set @s rpg_leg_cd 5
scoreboard players add @s ashes_level 1
execute if entity @s[scores={ashes_level=5..}] run scoreboard players set @s ashes_level 1
execute at @e[tag=rpg.legacy.target,limit=1] run particle minecraft:large_smoke ~ ~1 ~ 0.45 0.55 0.45 0.08 20 force
execute at @e[tag=rpg.legacy.target,limit=1] run particle minecraft:ash ~ ~1 ~ 0.4 0.5 0.4 0.05 18 force
execute as @e[tag=rpg.legacy.target,limit=1] run effect give @s minecraft:wither 2 0 true
execute if entity @s[scores={ashes_level=1}] at @e[tag=rpg.legacy.target,limit=1] run particle minecraft:dust_pillar{block_state:{Name:"minecraft:deepslate_coal_ore"}} ~ ~1 ~ 0.45 0.55 0.45 0.15 24 force
execute if entity @s[scores={ashes_level=1}] run playsound minecraft:item.mace.smash_air player @s ~ ~ ~ 0.75 0.85
execute if entity @s[scores={ashes_level=2}] at @e[tag=rpg.legacy.target,limit=1] run particle minecraft:sweep_attack ~ ~1 ~ 0.8 0.6 0.8 0 22 force
execute if entity @s[scores={ashes_level=2}] run playsound minecraft:item.mace.smash_ground player @s ~ ~ ~ 0.8 0.9
execute if entity @s[scores={ashes_level=3}] at @e[tag=rpg.legacy.target,limit=1] run particle minecraft:squid_ink ~ ~1 ~ 0.65 0.7 0.65 0.08 38 force
execute if entity @s[scores={ashes_level=3}] run playsound minecraft:item.mace.smash_ground_heavy player @s ~ ~ ~ 0.8 0.75
execute if entity @s[scores={ashes_level=4}] at @e[tag=rpg.legacy.target,limit=1] run particle minecraft:flash{color:7563296} ~ ~1 ~ 0 0 0 0 1 force
execute if entity @s[scores={ashes_level=4}] at @e[tag=rpg.legacy.target,limit=1] run particle minecraft:dust_color_transition{from_color:[0.35,0.42,0.12],to_color:[0.08,0.08,0.05],scale:2.2} ~ ~1 ~ 0.8 0.9 0.8 0.06 55 force
execute if entity @s[scores={ashes_level=4}] run damage @e[tag=rpg.legacy.target,limit=1] 3 minecraft:magic by @s
execute if entity @s[scores={ashes_level=4}] run playsound minecraft:entity.blaze.shoot player @s ~ ~ ~ 0.9 0.55
