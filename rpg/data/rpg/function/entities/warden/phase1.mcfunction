
execute as @e[tag=devil] at @s run function rpg:entities/warden/phase1_entity
# 旧实现遍历所有实体的 attacker；实际只需揭露攻击恶魔的人。
execute as @e[tag=devil] on attacker at @s run function rpg:entities/warden/reveal_attacker
