scoreboard players add @s rpg_ex_xp 50
function rpg:quest/title/get_summit
loot give @s loot rpg:world/bp_epic_any
tellraw @a[distance=0..] ["",{"text":"〖失乐园・登顶〗","color":"#E0483C","bold":true,"italic":false},{"text":" 𝔖𝔲𝔪𝔪𝔦𝔱","color":"#8F7430","bold":false,"italic":false},{"text":"  二十层都在你脚下。","color":"#9C9A94","bold":false,"italic":false}]
