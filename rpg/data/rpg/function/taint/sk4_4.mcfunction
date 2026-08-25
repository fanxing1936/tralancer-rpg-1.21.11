execute if entity @s[tag=rpg.ch1.boss] at @s as @a[tag=rpg.ch1.member,tag=rpg.ch1.party,tag=rpg.holy,distance=..18,gamemode=!spectator] if score @s rpg_ch1_id = @e[type=minecraft:vindicator,tag=rpg.ch1.boss,sort=nearest,limit=1,distance=..18] rpg_ch1_id run function rpg:campaign/beelzebub/witness/skill4
# 携圣器亲历这一招，记下一份不可重复的罪证。
execute at @s as @a[tag=rpg.holy,distance=..18,gamemode=!spectator] run function rpg:inquest/clue/4_4
execute at @s as @a[distance=..14,gamemode=!spectator,gamemode=!creative] run function rpg:hud/demon/m19
# 腐宴 —— 宴席先腐烂，宾客才知道自己已经坐在盘中。
playsound minecraft:entity.generic.eat hostile @a[distance=..32] ~ ~ ~ 1 0.45
playsound minecraft:block.composter.fill_success hostile @a[distance=..28] ~ ~ ~ 1 0.55
particle spore_blossom_air ~ ~1.4 ~ 4 1.5 4 0.08 105
particle mycelium ~ ~0.8 ~ 4 1 4 0.16 92
execute as @a[distance=..8,gamemode=!spectator,gamemode=!creative] run function rpg:taint/sk4d_feast
