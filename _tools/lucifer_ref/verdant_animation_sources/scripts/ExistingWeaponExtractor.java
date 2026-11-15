import java.nio.file.*;
import java.util.*;
import java.util.stream.IntStream;
import java.awt.image.BufferedImage;
import javax.imageio.ImageIO;
import java.lang.reflect.*;
import com.google.gson.*;
import org.joml.*;
public class ExistingWeaponExtractor {
 public static class PixelSprite extends ilk {
  BufferedImage image;
  public PixelSprite(){super(null,null,null);}
  @Override public int b(){return image.getWidth();}
  @Override public int c(){return image.getHeight();}
  @Override public IntStream e(){return IntStream.of(0);}
  @Override public boolean a(int frame,int x,int y){return (image.getRGB(x,y)>>>24)==0;}
 }
 static List<Double> vec(Vector3fc v){return List.of((double)v.x(),(double)v.y(),(double)v.z());}
 public static void main(String[] args)throws Exception {
  Field uf=sun.misc.Unsafe.class.getDeclaredField("theUnsafe");uf.setAccessible(true);sun.misc.Unsafe unsafe=(sun.misc.Unsafe)uf.get(null);
  PixelSprite sprite=(PixelSprite)unsafe.allocateInstance(PixelSprite.class);sprite.image=ImageIO.read(Path.of(args[0]).toFile());
  Method generate=hqj.class.getDeclaredMethod("a",int.class,String.class,ilk.class);generate.setAccessible(true);
  List<hqb> elements=(List<hqb>)generate.invoke(null,0,"layer0",sprite);
  List<Object> out=new ArrayList<>();
  for(hqb e:elements){Map<String,Object> o=new LinkedHashMap<>();o.put("from",vec(e.a()));o.put("to",vec(e.b()));List<Object> faces=new ArrayList<>();
   for(var en:e.c().entrySet()) {iz d=en.getKey();hqc f=en.getValue();Map<String,Object> face=new LinkedHashMap<>();face.put("direction",d.n());face.put("uv_rectangle_16",List.of((double)f.d().a(),(double)f.d().b(),(double)f.d().c(),(double)f.d().d()));List<Object> corners=new ArrayList<>();
    for(int i=0;i<4;i++){Vector3f pos=hoa.a(d).a(i).a(e.a(),e.b());corners.add(Map.of("position_model_pixels",vec(pos),"uv_normalized",List.of((double)hqc.a(f.d(),f.e(),i),(double)hqc.b(f.d(),f.e(),i))));}
    face.put("corners",corners);faces.add(face);
   }o.put("faces",faces);out.add(o);
  }
  JsonObject cfg=JsonParser.parseString(Files.readString(Path.of(args[1]))).getAsJsonObject().getAsJsonObject("display").getAsJsonObject("thirdperson_righthand");
  Vector3f[] trs=new Vector3f[3];int n=0;for(String key:List.of("rotation","translation","scale")){JsonArray a=cfg.getAsJsonArray(key);trs[n++]=new Vector3f(a.get(0).getAsFloat(),a.get(1).getAsFloat(),a.get(2).getAsFloat());}trs[1].div(16);
  hqk transform=new hqk(trs[0],trs[1],trs[2]);fzm stack=new fzm();transform.a(false,stack.c());Matrix4f mat=stack.c().a();List<Object> rows=new ArrayList<>();for(int r=0;r<4;r++){List<Double> row=new ArrayList<>();for(int c=0;c<4;c++)row.add((double)mat.get(c,r));rows.add(row);}
  Map<String,Object> result=new LinkedHashMap<>();result.put("method","Direct invocation of local Minecraft 1.21.11 ItemModelGenerator.processFrames and ItemTransform.apply; texture transparency supplied read-only from existing PNG via SpriteContents subclass.");result.put("texture_size",List.of(sprite.b(),sprite.c()));result.put("elements",out);result.put("thirdperson_righthand_matrix_from_unit_model",rows);
  Files.writeString(Path.of(args[2]),new GsonBuilder().setPrettyPrinting().create().toJson(result));System.out.println("Exported "+elements.size()+" generated elements");
 }
}