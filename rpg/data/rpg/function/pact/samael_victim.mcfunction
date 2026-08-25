# on attacker 会把 @s 换成攻击者；先给真正的受击者挂一个同步标签，
# 否则用 distance=..1,limit=1 会在拥挤的战团里毒到旁边那个实体。
tag @s add rpg.samael.victim
execute on attacker if entity @s[tag=rpg.pact,scores={rpg_pact=5}] run function rpg:pact/samael_hit
tag @s remove rpg.samael.victim
