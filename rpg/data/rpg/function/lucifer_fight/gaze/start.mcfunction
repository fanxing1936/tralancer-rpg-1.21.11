execute if entity @s[tag=rpg.advent] at @s as @a[tag=rpg.holy,distance=..18,gamemode=!spectator] run function rpg:inquest/clue/1_5
execute at @s as @a[distance=..14,gamemode=!spectator,gamemode=!creative] run function rpg:hud/demon/m49
function rpg:lucifer_p2/play/jungleabomination_vineattackidle
playsound minecraft:block.sculk_shrieker.shriek hostile @a[distance=..32] ~ ~ ~ 0.9 0.6
execute positioned ~ ~8.4 ~ run function rpg:lucifer_fight/gaze/eye
