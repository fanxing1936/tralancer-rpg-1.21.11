tellraw @a[tag=rpg.tw.in] ["",{"text":"〖","color":"#C9A646","bold":true,"italic":false},{"text":"神父","color":"#C9A646","bold":true,"italic":false},{"text":"〗","color":"#C9A646","bold":true,"italic":false},{"text":" 𝔉𝔞𝔱𝔥𝔢𝔯","color":"#8F7430","italic":false},{"text":"  天亮了。它们回到土里去了。","color":"#9C9A94","italic":false,"hover_event":{"action":"show_text","value":{"text":"Dawn. They've gone back into the earth.","color":"#8F7430","italic":false}}}]
playsound rpg:vo.town.ho04 voice @a[tag=rpg.tw.in] ~ ~ ~ 1 1
execute if score #tod rpg_te matches 13000..23000 run time set 23500
function rpg:town/ev/win
