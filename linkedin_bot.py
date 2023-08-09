from linkedin_utils import *
import pandas as pd


def get_ind(company_linkedin):
    try:
        driver.get(company_linkedin + '/about')
        time.sleep(2)
        scroll_to_bottom()
        scroll_to_half()
        scroll_to_top()
        time.sleep(2)
        ind = wait_for_element_to_load(By.XPATH,"(//dt[contains(.,'Industry')]//following-sibling::dd)[1]").text
        print(ind)
        return ind
    except :
        return None

csv_name = str(input("Enter csv name: "))
df = pd.read_csv(csv_name)

df1 = df.assign(company_industry=df['company_linkedin'].apply(get_ind))

print(df1)
df1.to_csv(f'with_industry_{csv_name}',index=False)


