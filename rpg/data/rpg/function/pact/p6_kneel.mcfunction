effect give @s minecraft:slowness 5 255 true
effect give @s minecraft:weakness 5 2 true
effect give @s minecraft:glowing 5 0 true
particle dust_color_transition{from_color:[0.4,0.0,0.6],to_color:[0.0,0.0,0.0],scale:2} ~ ~1 ~ 0.3 0.6 0.3 0.05 16
damage @s 4 minecraft:magic by @a[tag=rpg.pact.cast,limit=1,sort=nearest]
