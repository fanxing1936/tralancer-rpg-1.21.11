function rpg:inquest/stability/hit10
scoreboard players add @s rpg_ex_time 60
effect give @a[distance=..8,gamemode=!spectator] minecraft:slowness 6 2 true
effect give @a[distance=..8,gamemode=!spectator] minecraft:mining_fatigue 6 1 true
tellraw @a[distance=..16,gamemode=!spectator] ["",{"text":"〖反仪式・怠惰〗","color":"#8C90A1","bold":true,"italic":false},{"text":" 𝔖𝔩𝔬𝔱𝔥","color":"#8F7430","bold":false,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"亚巴顿令时间停滞，宣判延后了三秒。","color":"#9C9A94","italic":false}]
particle ash ~ ~0.7 ~ 2.5 0.4 2.5 0.02 55 normal
