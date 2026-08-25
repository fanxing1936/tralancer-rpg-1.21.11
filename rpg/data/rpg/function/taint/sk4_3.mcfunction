execute if entity @s[tag=rpg.ch1.boss] at @s as @a[tag=rpg.ch1.member,tag=rpg.ch1.party,tag=rpg.holy,distance=..18,gamemode=!spectator] if score @s rpg_ch1_id = @e[type=minecraft:vindicator,tag=rpg.ch1.boss,sort=nearest,limit=1,distance=..18] rpg_ch1_id run function rpg:campaign/beelzebub/witness/skill3
# 携圣器亲历这一招，记下一份不可重复的罪证。
execute at @s as @a[tag=rpg.holy,distance=..18,gamemode=!spectator] run function rpg:inquest/clue/4_3
execute at @s as @a[distance=..14,gamemode=!spectator,gamemode=!creative] run function rpg:hud/demon/m18
# 蝇群 —— 苍蝇王名副其实。
playsound minecraft:entity.bee.loop_aggressive hostile @a[distance=..32] ~ ~ ~ 1 0.5
particle mycelium ~ ~1 ~ 2 1 2 0.3 80
execute at @s run function rpg:taint/sk4c_swarm
