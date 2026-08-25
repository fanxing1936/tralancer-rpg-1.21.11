execute if entity @s[tag=rpg.ch1.boss] at @s as @a[tag=rpg.ch1.member,tag=rpg.ch1.party,tag=rpg.holy,distance=..18,gamemode=!spectator] if score @s rpg_ch1_id = @e[type=minecraft:vindicator,tag=rpg.ch1.boss,sort=nearest,limit=1,distance=..18] rpg_ch1_id run function rpg:campaign/beelzebub/witness/skill5
# 携圣器亲历这一招，记下一份不可重复的罪证。
execute at @s as @a[tag=rpg.holy,distance=..18,gamemode=!spectator] run function rpg:inquest/clue/4_5
execute at @s as @a[distance=..14,gamemode=!spectator,gamemode=!creative] run function rpg:hud/demon/m20
# 饥啮 —— 万千张口只追最近的一份血肉。
playsound minecraft:entity.fox.bite hostile @a[distance=..32] ~ ~ ~ 1 0.7
particle ash ~ ~1 ~ 2.5 1 2.5 0.14 84
particle damage_indicator ~ ~1 ~ 2 0.8 2 0.08 36
execute as @a[distance=..10,limit=1,sort=nearest,gamemode=!spectator,gamemode=!creative] run function rpg:taint/sk4e_bite
