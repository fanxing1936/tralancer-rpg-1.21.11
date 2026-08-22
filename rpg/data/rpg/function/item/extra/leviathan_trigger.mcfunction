# 利维坦［沉锚］—— 由 rpg:advancement/item/leviathan 在右键使用时触发。
# 代价是血而不是经验，所以先量一次生命：不够就拒绝，而不是把人送走。
# （包里其余主动技能在付不起代价时也是这个反应，一声 villager.no。）
advancement revoke @s only rpg:item/leviathan
execute store result score @s rpg_levi_hp run data get entity @s Health
execute if entity @s[scores={rpg_levi_hp=..10}] run playsound minecraft:entity.villager.no player @s
execute if entity @s[scores={rpg_levi_hp=11..}] run function rpg:item/extra/leviathan_cast
