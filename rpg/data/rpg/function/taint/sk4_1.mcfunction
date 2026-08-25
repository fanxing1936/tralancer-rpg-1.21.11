execute if entity @s[tag=rpg.ch1.boss] at @s as @a[tag=rpg.ch1.member,tag=rpg.ch1.party,tag=rpg.holy,distance=..18,gamemode=!spectator] if score @s rpg_ch1_id = @e[type=minecraft:vindicator,tag=rpg.ch1.boss,sort=nearest,limit=1,distance=..18] rpg_ch1_id run function rpg:campaign/beelzebub/witness/skill1
# 携圣器亲历这一招，记下一份不可重复的罪证。
execute at @s as @a[tag=rpg.holy,distance=..18,gamemode=!spectator] run function rpg:inquest/clue/4_1
execute at @s as @a[distance=..14,gamemode=!spectator,gamemode=!creative] run function rpg:hud/demon/m16
# 余烬 —— 前方喷灰，吸进去的人饿得站不住。
playsound minecraft:entity.blaze.shoot hostile @a[distance=..32] ~ ~ ~ 1 0.5
execute at @s anchored eyes facing entity @a[limit=1,sort=nearest,gamemode=!spectator,gamemode=!creative] feet run function rpg:taint/sk4_cone
