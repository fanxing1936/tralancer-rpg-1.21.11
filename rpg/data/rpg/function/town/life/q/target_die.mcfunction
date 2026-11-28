kill @e[type=minecraft:block_display,tag=rpg.tl.tdisp,distance=..1]
kill @s
execute unless entity @e[type=minecraft:interaction,tag=rpg.tl.target] as @a[tag=rpg.tl.bet] run function rpg:town/life/q/bet_end
