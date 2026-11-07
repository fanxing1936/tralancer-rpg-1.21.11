effect give @s minecraft:slowness 6 6 true
effect give @s minecraft:mining_fatigue 6 2 true
particle wax_on ~ ~0.6 ~ 0.3 0.4 0.3 0.05 10
summon minecraft:experience_orb ~ ~1 ~ {Value:8}
damage @s 8 minecraft:magic by @a[tag=rpg.pact.cast,limit=1,sort=nearest]
