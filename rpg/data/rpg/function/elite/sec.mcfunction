scoreboard players set #t rpg_el 0
bossbar set rpg:elite_champion_bar players
execute as @e[tag=rpg.el] at @s run function rpg:elite/each
function rpg:pl/bar/all
