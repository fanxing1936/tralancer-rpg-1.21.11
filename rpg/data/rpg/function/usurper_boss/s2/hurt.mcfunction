# 二阶段没有原作原声（首席附魔师没有可用原件）：受击用原版唤魔者的声音压低
playsound minecraft:entity.evoker.hurt hostile @a[distance=..32] ~ ~ ~ 1 0.7
playsound minecraft:block.amethyst_block.hit hostile @a[distance=..32] ~ ~ ~ 0.6 0.8
# 致命一击可能刚吃掉副手的死亡保护：补回去，下次照样挡
item replace entity @s weapon.offhand with minecraft:paper[minecraft:death_protection={},minecraft:item_model="rpg:empty"]
scoreboard players operation #lost rpg_ub /= #two rpg_ub
execute if entity @s[tag=rpg.usb.exposed] run return run function rpg:usurper_boss/s2/extra
execute if entity @e[tag=rpg.usb.guard,distance=..120] run function rpg:usurper_boss/s2/refund
