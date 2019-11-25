import pandas as pd
import bokeh
from bokeh.io import curdoc,show,output_file,push_notebook
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, DataRange1d\
    , Select, TableColumn, DataTable,TextInput, Button
from bokeh.models.callbacks import CustomJS

df = pd.read_csv('C:/Users/wjian/Desktop/ANLY501/project_folder/final_data.csv')

nutri_lu = df[['id','calories','total_fat','sugar','sodium','protein','saturated_fat','carbohydrates']]
nutri_lu = nutri_lu[nutri_lu['calories'] <= 1000]


entrees = nutri_lu[nutri_lu['calories'] >= 500].reset_index()

def combo(entree_id, calory):
    item = nutri_lu[nutri_lu['id'] == entree_id].reset_index()
    calo = item.loc[0, 'calories']
    choice = nutri_lu[nutri_lu['calories'] <= calory - calo]
    rd_choice = choice.sample(n=1).reset_index()

    if rd_choice.loc[0, 'calories'] + calo <= calory:
        choice_2 = nutri_lu[nutri_lu['calories'] <= calory - calo - rd_choice.loc[0, 'calories']].sample(
            n=1).reset_index()
        return [entree_id, rd_choice.loc[0, 'id'], choice_2.loc[0, 'id']]

    else:
        return [entree_id, rd_choice.loc[0, 'id']]

######
source = ColumnDataSource(data=dict())

#The update function
def update():
    entree = int(entree_id.value)
    calories = int(calories_input.value)
    combo_id = combo(entree,calories)
    current = df[df['id'].isin(combo_id)]
    source.data = {
        'name': current.name,
        'id': current.id,
        'ingredients': current.ingredients,
        'cuisine': current.cuisine,
        'score': current.score,
        'minutes': current.minutes,
        'tags': current.tags,
        'n_steps': current.n_steps,
        'steps': current.steps,
        'n_ingredients': current.n_ingredients,
        'calories': current.calories,
        'total_fat': current.total_fat,
        'sugar': current.sugar,
        'sodium':current.sodium,
        'protein':current.protein,
        'saturated_fat': current.saturated_fat,
        'carbohydrates':current.carbohydrates,
        'rating':current.rating,
        'num_review':current.num_review,
        'contributor_id':current.contributor_id,
        'submitted':current.submitted
    }

#callback
callback = CustomJS(args=dict(source=source), code="""
    var data = source.data;
    source.change.emit();
""")

entree = '31490'
calories = '1000'

#control pf select bar
entree_id = TextInput(title='Please type in the entree id',value=entree)
entree_id.on_change('value', lambda attr, old, new: update())
calories_input = TextInput(title='Please type in the target total calories',value=calories)
calories_input.on_change('value', lambda attr, old, new: update())
button = Button(label='Reroll',button_type='success')
button.on_click(lambda :update())
#button.js_on_click(lambda :callback)

#get all data
columns =[]
for x in df:
    columns.append(TableColumn(field=x, title=x))

data_table = DataTable(source = source, columns = columns, width = 2000)

controls = column(entree_id,calories_input, button)

curdoc().add_root(column(controls, data_table))
curdoc().title = 'Combo'

#output_file('combo.html')


#initialization
update()
#show(column(controls,data_table))
