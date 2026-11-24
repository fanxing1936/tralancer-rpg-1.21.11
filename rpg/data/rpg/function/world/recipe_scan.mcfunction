scoreboard players set #t rpg_wl_rl 0
execute as @a if data entity @s recipeBook.recipes[0] run recipe take @s *
function rpg:world/relic/scan
execute as @a[scores={rpg_ident=4,rpg_sef=3..},tag=!rpg.wl.book] run function rpg:world/pact_book
