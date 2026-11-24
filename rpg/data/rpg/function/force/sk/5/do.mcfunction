playsound minecraft:block.amethyst_block.chime player @a[distance=..16] ~ ~ ~ 1 1.4
function rpg:force/ray/bless/go
execute unless score #stop rpg_fo matches 1 run function rpg:force/sk/5/heal
