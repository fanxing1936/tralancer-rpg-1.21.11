tp @a[tag=rpg.pact.cast,limit=1] ^ ^ ^-1
particle soul_fire_flame ~ ~1 ~ 0.6 0.8 0.6 0.08 24
particle crit ~ ~1 ~ 0.6 0.8 0.6 0.2 24
playsound minecraft:entity.player.attack.crit player @a[distance=..24] ~ ~ ~ 1 0.7
effect give @s minecraft:wither 5 1 true
damage @s 14 minecraft:magic by @a[tag=rpg.pact.cast,limit=1,sort=nearest]
