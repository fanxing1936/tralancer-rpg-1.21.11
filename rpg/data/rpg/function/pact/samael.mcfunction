# 暴怒的毒。走 rpg.hurt + on attacker，与包里其余被动同一形状。
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[tag=rpg.pact,scores={rpg_pact=5}] run effect give @e[distance=..1,limit=1] minecraft:poison 6 1 true
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[tag=rpg.pact,scores={rpg_pact=5}] run particle dust{color:[0.36,0.62,0.16],scale:1} ~ ~1 ~ 0.3 0.4 0.3 0.02 8
