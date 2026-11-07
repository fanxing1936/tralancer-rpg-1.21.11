# 同 samael_victim：先锁定受击者，再换到攻击者身上判柱印。
tag @s add rpg.seal.victim
execute on attacker if entity @s[tag=rpg.pact.onhit] run function rpg:pact/seal/hit
tag @s remove rpg.seal.victim
