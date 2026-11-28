function rpg:town/ev/board_text
function rpg:town/ev/priest_info_m with storage rpg:town ev
tellraw @s ["",{"text":"〖","color":"#C9A646","bold":true,"italic":false},{"text":"神父","color":"#C9A646","bold":true,"italic":false},{"text":"〗","color":"#C9A646","bold":true,"italic":false},{"text":" 𝔉𝔞𝔱𝔥𝔢𝔯","color":"#8F7430","italic":false},{"text":"  要学驱魔，先学会看。恶魔留下的痕迹，比它本身好找。","color":"#9C9A94","italic":false,"hover_event":{"action":"show_text","value":{"text":"To learn exorcism, first learn to look. A demon's traces are easier to find than the demon.","color":"#8F7430","italic":false}}}]
playsound rpg:vo.town.pr07 voice @s ~ ~ ~ 1 1
