# 时候到了，它自己散掉 —— 不是被你打退的。
#
# 先把探针一起收走：自己散掉的**不炸**，炸的只有被打死的。
# 别西卜外观（add_beelzebub.py）
# 利维坦外观（add_leviathan_model.py）
execute if entity @s[tag=rpg.lv] run playsound rpg:leviathan.laugh hostile @a[distance=..32] ~ ~ ~ 1.2 0.7
execute if entity @s[tag=rpg.bz] run playsound rpg:beelzebub.poff hostile @a[distance=..32] ~ ~ ~ 1.2 1
execute if entity @s[tag=rpg.bz] run playsound rpg:beelzebub.teleport_out hostile @a[distance=..32] ~ ~ ~ 1.2 0.8
execute on passengers run kill @s
particle sculk_soul ~ ~1 ~ 0.5 0.9 0.5 0.08 60
particle large_smoke ~ ~1 ~ 0.4 0.8 0.4 0.05 40
particle squid_ink ~ ~1 ~ 0.4 0.8 0.4 0.05 30
playsound minecraft:entity.evoker.death hostile @a[distance=..32] ~ ~ ~ 1 0.6
kill @s
