$scoreboard players set @s rpg_ps_$(n) $(s)
function rpg:sephira/bonus/apply
playsound minecraft:item.book.page_turn player @s ~ ~ ~ 1 0.8
playsound minecraft:block.enchantment_table.use player @s ~ ~ ~ 0.8 1.3
$scoreboard players set #pn rpg_pa $(n)
function rpg:paths/page/any
