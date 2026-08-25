# 携圣器亲历这一招，记下一份不可重复的罪证。
execute at @s as @a[tag=rpg.holy,distance=..18,gamemode=!spectator] run function rpg:inquest/clue/6_5
execute at @s as @a[distance=..14,gamemode=!spectator,gamemode=!creative] run function rpg:hud/demon/m30
# 欲障 —— 紫幕落下，真实与渴望只剩一层薄纱。
playsound minecraft:block.respawn_anchor.ambient hostile @a[distance=..32] ~ ~ ~ 1 0.55
particle portal ~ ~1 ~ 4 1.5 4 0.55 120
particle reverse_portal ~ ~1 ~ 3.5 1.2 3.5 0.25 84
execute as @a[distance=..10,gamemode=!spectator,gamemode=!creative] run function rpg:taint/sk6e_veil
