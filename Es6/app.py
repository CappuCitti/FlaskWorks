from flask import *
import folium
import geopandas as gpd

app = Flask(__name__)

quartieri = gpd.read_file("./static/files/ds964_nil_wm.zip")
fontanelle = gpd.read_file("./static/files/Fontanelle.zip")


@app.route('/', methods=['GET'])
def home():
  return render_template('index.html')


@app.route('/map', methods=['GET'])
def map():
  return render_template('map.html')


@app.route('/visualizza', methods=['GET'])
def view():
  my_map = folium.Map(location=[45.46409946028481, 9.19187017173384], tiles='cartodbpositron', zoom_start=12)

  shapes = gpd.GeoSeries(quartieri['geometry']).simplify(tolerance=0.000)
  shapes = shapes.to_json()
  shapes = folium.GeoJson(data=shapes, style_function=lambda x: {'fillColor': 'gray'})

  shapes.add_to(my_map)

  my_map.save("templates/map.html")

  return render_template('getMap.html', navbar_content='get_all')


@app.route('/ricerca', methods=['GET'])
def search():
  my_map = folium.Map(location=[45.46409946028481, 9.19187017173384], tiles='cartodbpositron', zoom_start=12)

  my_map.save("templates/map.html")

  return render_template('getMap.html', navbar_content='search')


@app.route('/ricerca', methods=['POST'])
def add_component():

  status = 'Il quartiere non esiste!'
  process = False


  req = request.form.get("nil").upper()
  res = quartieri[quartieri["NIL"] == req]
  if len(res) != 0:
    my_map = folium.Map(location=[45.46409946028481, 9.19187017173384], tiles='cartodbpositron', zoom_start=12)
    shape = folium.GeoJson(data=res['geometry'], style_function=lambda x: {'fillColor': 'gray'})
    shape.add_to(my_map)
    my_map.save("templates/map.html")

    process = True
    status = res['NIL'].values[0].title()
  else:
    my_map = folium.Map(location=[45.46409946028481, 9.19187017173384], tiles='cartodbpositron', zoom_start=12)
    my_map.save("templates/map.html")

  return render_template('getMap.html', navbar_content='search', process=process, status=status)


@app.route('/scelta', methods=['GET'])
def choice():
  my_map = folium.Map(location=[45.46409946028481, 9.19187017173384], tiles='cartodbpositron', zoom_start=12)
  my_map.save("templates/map.html")

  series = quartieri["NIL"].sort_values(ascending=True).apply(lambda x: x.title())

  return render_template('getMap.html', navbar_content='choice', shapes=series, selected=series.iloc[0])


@app.route('/scelta', methods=['POST'])
def choice_return():
  req = request.form.get("shapes").upper()
  res = quartieri[quartieri["NIL"] == req]

  my_map = folium.Map(location=[45.46409946028481, 9.19187017173384], tiles='cartodbpositron', zoom_start=12)
  shape = folium.GeoJson(data=res['geometry'], style_function=lambda x: {'fillColor': 'gray'})
  shape.add_to(my_map)
  my_map.save("templates/map.html")

  return render_template('getMap.html', navbar_content='choice', shapes=quartieri["NIL"].sort_values(ascending=True).apply(lambda x: x.title()), selected=req)


@app.route('/fontanelle', methods=['GET'])
def choice_f():
  my_map = folium.Map(location=[45.46409946028481, 9.19187017173384], tiles='cartodbpositron', zoom_start=12)
  my_map.save("templates/map.html")

  series = quartieri["NIL"].sort_values(ascending=True).apply(lambda x: x.title())

  return render_template('getMap.html', navbar_content='choice_f', shapes=series, selected=series.iloc[0])


@app.route('/fontanelle', methods=['POST'])
def choice_return_f():
  req = request.form.get("shapes").upper()
  res = quartieri[quartieri["NIL"] == req]

  my_map = folium.Map(location=[45.46409946028481, 9.19187017173384], tiles='cartodbpositron', zoom_start=12)

  shape = folium.GeoJson(data=res['geometry'], style_function=lambda x: {'fillColor': 'gray'})
  shape.add_to(my_map)

  res_f = fontanelle[fontanelle.within(res.geometry.squeeze())]

  status = 'Non sono presenti fontanelle in questa zona!'
  process = False
  if len(res_f) != 0:
    shape = folium.GeoJson(data=res_f['geometry'], style_function=lambda x: {'fillColor': 'blue'})
    status = res_f['geometry']
    process = True
  shape.add_to(my_map)

  my_map.save("templates/map.html")

  return render_template('getMap.html', navbar_content='choice_f', shapes=quartieri["NIL"].sort_values(ascending=True).apply(lambda x: x.title()), selected=req, status=status)


if __name__ == "__main__":
  app.run(debug=True, host="0.0.0.0", port=5004)