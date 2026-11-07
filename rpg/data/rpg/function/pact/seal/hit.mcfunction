execute if entity @s[tag=rpg.pact.s4] as @e[tag=rpg.seal.victim,limit=1] run effect give @s minecraft:weakness 3 0 true
execute if entity @s[tag=rpg.pact.s5] as @e[tag=rpg.seal.victim,limit=1] run function rpg:pact/seal/finish
