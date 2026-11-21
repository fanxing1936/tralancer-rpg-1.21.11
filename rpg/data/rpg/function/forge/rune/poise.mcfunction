scoreboard players add #pct rpg_fg 50
tag @a[tag=rpg.fg.atk,limit=1] add rpg.fg.from
function rpg:forge/fx/push
tag @a[tag=rpg.fg.from] remove rpg.fg.from
playsound minecraft:entity.player.attack.knockback player @a[distance=..12] ~ ~ ~ 1 0.8
