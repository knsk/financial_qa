# import sys
import os
import argparse
from openai import OpenAI
from unstructured.partition.html import partition_html
from sqlalchemy import asc, desc, and_, not_
from models import session, Article

def finantial_result_overview_prompt(text: str ,company_name: str) -> str:
  FINANCIAL_RESULT_OVERVIEW = """下記の情報から{company_name}の決算について教えてください。
  ```
  {text}
  ```"""
  return FINANCIAL_RESULT_OVERVIEW.format(company_name=company_name, text=text)

def management_analisys_prompt(text: str, company_name: str) -> str:
  MANAGEMENT_ANALISYS = """下記の情報から{company_name}の決算データを分析して今後の経営戦略を立案してください。
  ```
  {text}
  ```"""
  return MANAGEMENT_ANALISYS.format(company_name=company_name, text=text)

def management_analisys_with_mission_prompt(text: str, company_name: str, mission: str="") -> str:
  MANAGEMENT_ANALISYS="""あなたは{company_name}の代表取締役CEOです。下記のミッションと決算情報に基づいて今後の経営方針について熱意を持って伝えてください。
  ミッション：
  ```
  {mission}
  ```

  決算情報：
  ```
  {text}
  ```"""
  return MANAGEMENT_ANALISYS.format(company_name=company_name, mission=mission, text=text)


def retrieve(keyword: str, max_length: int) -> str:
  # TODO Consider utilizing Vector DB
  if keyword == '楽天':
    articles = session.query(Article).filter(and_(Article.text.ilike(f"%{keyword}%"), not_(Article.text.ilike('%東京楽天地%')))).order_by(desc(Article.published_at)).all()
  else:
    articles = session.query(Article).filter(Article.text.ilike(f"%{keyword}%")).order_by(desc(Article.published_at)).all()
  result = ""
  for article in articles:
    # print(f"len(result): {len(result)}")
    if len(result) < max_length:
      result = f"{result}\n\n============\n\n{article.text}"
    else:
      return result
  return result
  

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('-n', '--name', type=str, help='Company name to ask', required=True)
  parser.add_argument('-o', '--overview', action='store_true', help='Flag for asking finantial result overview')
  parser.add_argument('-a', '--analyze', action='store_true', help='Flag for asking management analisys')
  parser.add_argument('-c', '--ceo', action='store_true', help='Flag for asking CEO analisys')
  parser.add_argument('-u', '--url', type=str, help='URL for mission statement page')

  args = parser.parse_args()

  company_name = args.name
  client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
  MAX_LENGTH=128000
  text = retrieve(company_name, MAX_LENGTH)
  if args.overview or (not args.analyze and not args.ceo):
    prompt = finantial_result_overview_prompt(text, company_name)
    print(f"Q: {company_name}の決算について教えてください。")
  elif args.analyze:
    prompt = management_analisys_prompt(text, company_name)
    print(f"Q: {company_name}の決算情報に基づいて今後の経営戦略を立案してください。")
  elif args.ceo and args.url:
    mission_url = args.url
    elements = partition_html(url=mission_url)
    mission = "\n".join([element.text for element in elements])
    prompt = management_analisys_with_mission_prompt(text, company_name, mission)
    # print(f"prompt:")
    # print(f"{prompt}")
    print(f"Q: {company_name}のCEOとしてミッションと決算情報に基づいて今後の経営方針について教えてください。")

  print()
  print("A:")
  stream = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": prompt,
        }
    ],
    model="gpt-4-turbo",
    stream=True
  )

  for chunk in stream:
    print(chunk.choices[0].delta.content or "", end="")
  print()


if __name__ == '__main__':
  main()
