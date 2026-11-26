# 手上的档案头颅（玩家头颅）换成同名、同头像的纸（as 玩家）
data remove storage rpg:panel head
data modify storage rpg:panel head.p set from entity @s SelectedItem.components."minecraft:profile"
item replace entity @s weapon.mainhand with minecraft:paper[minecraft:item_model="rpg:panel/head",minecraft:consumable={consume_seconds:100000f,animation:"none",has_consume_particles:false,sound:"minecraft:intentionally_empty"},minecraft:custom_data={player_tag:1b},minecraft:max_stack_size=1,minecraft:enchantment_glint_override=true]
execute if data storage rpg:panel head.p run function rpg:panel/v2/head_copy with storage rpg:panel head
