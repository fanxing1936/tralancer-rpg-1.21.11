# 立图腾 —— 由 rpg:item/rite 在「以驱魔图腾右击方块」时触发。
# 图腾本体用 item_display：没有 AI、没有碰撞，只是一件立在那儿的东西。
advancement revoke @s only rpg:item/rite
execute if entity @s[scores={rpg_rite=1..}] run return 0

# 手里必须真的是驱魔图腾。item_used_on_block 天生promiscuous ——
# "对方块使用物品"把**放方块**也算在内，所以正确性不该全押在进度的断言上，
# 这里再验一道。
execute unless items entity @s weapon.mainhand minecraft:totem_of_undying[minecraft:custom_data~{totem_tag:1b}] run return 0

scoreboard players set @s rpg_rite 10
clear @s minecraft:totem_of_undying[minecraft:custom_data~{totem_tag:1b}] 1
execute at @s anchored eyes positioned ^ ^ ^2 run function rpg:rite/place
